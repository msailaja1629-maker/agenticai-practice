import os
import boto3
from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub

load_dotenv()

class InfraAgent:
    def __init__(self):
        # Initialize Bedrock LLM (Ensure Model ID is in .env)
        self.llm = ChatBedrock(
            model_id=os.getenv("LLM_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            model_kwargs={"temperature": 0}
        )
        
        # Define Tools
        self.tools = self._setup_tools()
        
        # Pull the ReAct Prompt from LangChain Hub
        # Fallback included if Hub is unreachable
        try:
            prompt = hub.pull("hwchase17/react")
        except Exception:
            from langchain_core.prompts import PromptTemplate
            template = "Answer the following: {tools}. Question: {input}. Thought:{agent_scratchpad}"
            prompt = PromptTemplate.from_template(template)
        
        # Create the Agent
        agent = create_react_agent(self.llm, self.tools, prompt)
        
        # Create the Executor
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def _setup_tools(self):
        return [
            Tool(name="ComputeInventory", func=self.get_compute, description="Lists EC2 instances."),
            Tool(name="StorageInventory", func=self.get_storage, description="Lists S3 buckets."),
            Tool(name="DatabaseInventory", func=self.get_rds, description="Lists RDS instances."),
            Tool(name="ComplianceCheck", func=self.get_compliance, description="Checks AWS Config for non-compliant resources."),
            Tool(name="CostOptimizer", func=self.get_costs, description="Finds unassociated Elastic IPs.")
        ]

    # --- AWS SDK Logic (Boto3) ---
    def get_compute(self, _=None):
        ec2 = boto3.client('ec2')
        try:
            instances = ec2.describe_instances()
            res = [f"EC2: {i['InstanceId']} ({i['State']['Name']})" for r in instances['Reservations'] for i in r['Instances']]
            return "\n".join(res) or "No EC2 instances found."
        except Exception as e: return f"Error: {str(e)}"

    def get_storage(self, _=None):
        s3 = boto3.client('s3')
        try:
            buckets = [f"S3: {b['Name']}" for b in s3.list_buckets()['Buckets']]
            return "\n".join(buckets) or "No S3 buckets found."
        except Exception as e: return f"Error: {str(e)}"

    def get_rds(self, _=None):
        rds = boto3.client('rds')
        try:
            dbs = rds.describe_db_instances()['DBInstances']
            return "\n".join([f"RDS: {d['DBInstanceIdentifier']}" for d in dbs]) or "No RDS found."
        except Exception: return "Error fetching RDS."

    def get_compliance(self, _=None):
        config = boto3.client('config')
        try:
            rules = config.describe_compliance_by_config_rule(ComplianceTypes=['NON_COMPLIANT'])['ComplianceByConfigRules']
            return "\n".join([r['ConfigRuleName'] for r in rules]) or "Infrastructure is compliant."
        except Exception: return "AWS Config not accessible."

    def get_costs(self, _=None):
        ec2 = boto3.client('ec2')
        try:
            eips = ec2.describe_addresses()['Addresses']
            unassociated = [e['PublicIp'] for e in eips if 'InstanceId' not in e]
            return f"Found leak: Unassociated EIPs: {unassociated}" if unassociated else "No unassociated EIPs."
        except Exception: return "Error checking cost leaks."

    def ask(self, prompt):
        response = self.executor.invoke({"input": prompt})
        return response["output"]