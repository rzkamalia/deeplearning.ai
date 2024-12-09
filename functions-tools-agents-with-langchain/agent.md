## Agent
+ an agent is an LLM-based system that dynamically decides the control flow of an application, enabling it to handle complex problems. instead of following a fixed sequence of steps, agents use the LLM to make decisions like routing between paths, choosing which tools to use, or determining if additional work is needed to improve the output. this flexibility has led to various agent architectures that grant the LLM varying degrees of control in solving tasks.

+ a router is an agent architecture where an LLM makes a single decision from a set of predefined options. it provides limited control, as the LLM focuses on selecting one action or output from a narrow range of possibilities, often using specific strategies to guide its choice.

+ structured outputs with LLMs work by providing a specific format or schema that the LLM should follow in its response. common methods to achieve structured outputs include:
    + in prompt
    + using output parsers
    + tool calling

+ ReAct is a popular architecture that combines these with three key features: `tool calling`, `memory` for retaining information, and `planning` for multi-step goals.