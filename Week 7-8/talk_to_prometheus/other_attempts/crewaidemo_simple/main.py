# Entry point for Talk to Prometheus
print("Importing modules...")
import sys
from crewai import Crew, Process
from tasks import PlanTask, ExecuteTask, AnalyzeTask
print("Modules imported successfully.")

def main():
    print("Starting CrewAI - Talk to Prometheus...")
    crew = Crew(
        agents=[
            PlanTask.agent,
            ExecuteTask.agent,
            AnalyzeTask.agent
        ],
        tasks=[PlanTask, ExecuteTask, AnalyzeTask],
        process=Process.sequential,
        verbose=True
    )
    print("CrewAI initialized successfully. now talk to prometheus!")
    query = "What is the average memory usage over the last 5 minutes?"
    # query = input("Ask prometheus: ")
    if len(query) > 5:
        result = crew.kickoff(inputs={"input": query})
        print(result)
    else:
        print("Please provide a more detailed query.")
        sys.exit(1)

if __name__ == "__main__":
    main()    