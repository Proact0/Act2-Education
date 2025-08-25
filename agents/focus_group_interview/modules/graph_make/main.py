from choose import StartGraph
from graphs.freetalk import freetalk_graph
from graphs.sequence import sequence_graph
from graphs.normal import normal_graph

if __name__ == "__main__":
    
    theme = "다크 모드의 장단점"

    startgraph = StartGraph()

    talk_type = startgraph.get_type(theme)

    print(talk_type.parsed.value)

    initial_state = {
        "messages": [
            (
                "user",
                theme
            )
        ]
    }

    if talk_type.parsed.value == "normal":
        events = normal_graph.stream(initial_state) 

    elif talk_type.parsed.value == "freetalk":
        events = freetalk_graph.stream(initial_state)

    elif talk_type.parsed.value == "sequence":
        events = sequence_graph.stream(initial_state)

    for event in events:
        print(event)