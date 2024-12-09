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