# Entry point for Talk to Prometheus
print("Importing modules...")
from langgraph import Graph
from tasks import PlanTask, ExecuteTask, AnalyzeTask
print("Modules imported successfully.")

def main():
    print("Initializing LangGraph workflow...")

    # Create the graph
    graph = Graph(
        tasks=[PlanTask, ExecuteTask, AnalyzeTask],
        connections=[
            (PlanTask, ExecuteTask),
            (ExecuteTask, AnalyzeTask)
        ]
    )

    # Execute the workflow
    query = input("Ask Prometheus: ")
    if len(query) > 5:
        result = graph.run(inputs={"input": query})
        print("Workflow completed. Results:")
        print(result)
    else:
        print("Please provide a more detailed query.")

if __name__ == "__main__":
    main()
