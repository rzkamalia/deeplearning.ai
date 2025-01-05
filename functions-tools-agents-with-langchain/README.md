## Agent
+ an agent is an LLM-based system that dynamically decides the control flow of an application, enabling it to handle complex problems. instead of following a fixed sequence of steps, agents use the LLM to make decisions like routing between paths, choosing which tools to use, or determining if additional work is needed to improve the output. this flexibility has led to various agent architectures that grant the LLM varying degrees of control in solving tasks.

+ a router is an agent architecture where an LLM makes a single decision from a set of predefined options. it provides limited control, as the LLM focuses on selecting one action or output from a narrow range of possibilities, often using specific strategies to guide its choice.

+ structured outputs with LLMs work by providing a specific format or schema that the LLM should follow in its response. common methods to achieve structured outputs include:
    + in prompt
    + using output parsers
    + tool calling

+ ReAct is a popular architecture that combines these with three key features: `tool calling`, `memory` for retaining information, and `planning` for multi-step goals.

## LangChain Expression Language (LCEL)
LCEL: LangChain composes chains of components. 
```
Chain = prompt | llm | OutputParser
```

Interface: 
+ components implement "Runnable" protocol.
+ common methos include:
    + invoke (synch) or ainvoke (asynch): which calls the runnable on a single input.
    + stream (synch) or astream (asynch): which calls it on a single input in stream's backer response.
    + batch (synch) or abatch (asynch): which calls it on list input.
+ common properties:
    + input_schema
    + output_schema
+ common I/O

| component     | input type                                | output type       |
|:-----         |:-----:                                    |-----:             |
| Prompt        | dictionary                                | prompt value      |
| Retriever     | single string                             | list of documnets |
| LLM           | string, list of messages or prompt value  | string            |
| ChatModel     | string, list of messages or prompt value  | ChatMessage       |
| Tool          | string or dictionary                      | tool dependent    |
| OutputParser  | output of LLM or ChatModel                | parser dependent  |

Why we shoud use LCEL?
+ Runnables support:
    + async, batch, and streaming support
    + fallbacks
    + parallelism
    + logging: langsmith

## Tagging and Extraction
Tagging: we pass in an unstructured piece of text along with some structured desciption, then we use LLM to generate some structured output.
Extraction: similar to tagging, but used for extracting multiple pieces of information, not for generate.