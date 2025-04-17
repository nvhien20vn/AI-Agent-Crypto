## 1. Tạo dự án
- Tạo 1 dự án theo mong muốn ở dưới vào @/nvhien-example1
- Xây dựng tôi 1 con AI-Agent với với mục đích phân tích và nghiên cứu về thị trường tiền số hằng ngày
- Sử dụng framework LangChain và LangGraph. Graph chỉ gồm 3 node là START, END và một node LLM.
- Có sử dụng memory trong langgraph
- Dễ dang mở rộng dự án thêm với các option trên dạng function calling custom

### 1.1 Cải tiến dự án
- Tôi thấy trên GPT, hay Gemini có tính năng deepsearch hay thực hiện bổ sung tính năng này cho tôi
- Tôi cần tạo thêm 1 số tool calling hay gợi ý tool calling cho tôi


### 1.2 Cải tiến v1
- Bổ sung thêm lưu trữ lịch sử bộ nhớ của prompt hay ngữ cảnh vào database
- Bổ sung thêm tool_calling : gợi ý giúp tôi 1 vài tool


### 1.3 cải tiến v2
- bỏ tính năng deepseaarch đi, chỉ sử dụng tool_calling tôi vừa mới thêm thôi


### 1.4 fixbug
- Khi tôi thực hiện hỏi về giá BTC Hôm nay bị lỗi => chạy ra kết quả rồi xong sau đó văng lỗi, tìm hiểu nguyên nhân tại sao

lỗi bị văng đây 
```
python nvhien-example1/main.py
Starting Crypto Market Analysis AI...

ℹ️  Tool Information:

Available Crypto Analysis Tools:
1. crypto_price: Get real-time cryptocurrency prices
   - Input: Coin symbol (e.g., 'BTC' or 'ETH')
   - Example: "What's the current price of BTC?"

2. crypto_news: Get latest cryptocurrency news
   - Input: Optional coin name for specific news
   - Example: "Show me the latest Bitcoin news"

3. web_search: Search for crypto-related information
   - Input: Search query
   - Example: "Search for cryptocurrency mining impact"

You: (Press Enter for default 'Analyze the crypto market.') What's the current price of BTC?
AI is thinking...
---AGENT NODE---
Routing to tools
---TOOLS NODE---
Tool calls: [{'name': 'crypto_price', 'args': {'__arg1': 'BTC'}, 'id': 'call_WZJmK4VPpI5IkLUMFNNf3pED', 'type': 'tool_call'}]
Executing tool: crypto_price with args: {'__arg1': 'BTC'}
Tool output: BTC/USD:
  Price: $84,221.97
  24h Change: 0.33%
  24h Volume: $19,511.99
---AGENT NODE---
Traceback (most recent call last):
  File "C:\Users\HO VAN ANH\Desktop\nvhien-AI-Agent\nvhien-example1\main.py", line 77, in <module>
    main()
    ~~~~^^
  File "C:\Users\HO VAN ANH\Desktop\nvhien-AI-Agent\nvhien-example1\main.py", line 50, in main    
    final_state = agent.invoke(state)
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\langgraph\pregel\__init__.py", line 2142, in invoke
    for chunk in self.stream(
                 ~~~~~~~~~~~^
        input,
        ^^^^^^
    ...<6 lines>...
        **kwargs,
        ^^^^^^^^^
    ):
    ^
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\langgraph\pregel\__init__.py", line 1797, in stream
    for _ in runner.tick(
             ~~~~~~~~~~~^
        loop.tasks.values(),
        ^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        get_waiter=get_waiter,
        ^^^^^^^^^^^^^^^^^^^^^^
    ):
    ^
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\langgraph\pregel\runner.py", line 230, in tick
    run_with_retry(
    ~~~~~~~~~~~~~~^
        t,
        ^^
    ...<4 lines>...
        },
        ^^
    )
    ^
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\langgraph\pregel\retry.py", line 40, in run_with_retry
    return task.proc.invoke(task.input, config)
           ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\langgraph\utils\runnable.py", line 546, in invoke
    input = step.invoke(input, config, **kwargs)
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\langgraph\utils\runnable.py", line 310, in invoke
    ret = context.run(self.func, *args, **kwargs)
  File "C:\Users\HO VAN ANH\Desktop\nvhien-AI-Agent\nvhien-example1\src\agent.py", line 33, in agent_node
    response = llm_with_tools.invoke(messages)
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\langchain_core\runnables\base.py", line 5440, in invoke
    return self.bound.invoke(
           ~~~~~~~~~~~~~~~~~^
        input,
        ^^^^^^
        self._merge_configs(config),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        **{**self.kwargs, **kwargs},
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\langchain_core\language_models\chat_models.py", line 331, in invoke
    self.generate_prompt(
    ~~~~~~~~~~~~~~~~~~~~^
        [self._convert_input(input)],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        **kwargs,
        ^^^^^^^^^
    ).generations[0][0],
    ^
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\langchain_core\language_models\chat_models.py", line 894, in generate_prompt
    return self.generate(prompt_messages, stop=stop, callbacks=callbacks, **kwargs)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\langchain_core\language_models\chat_models.py", line 719, in generate
    self._generate_with_cache(
    ~~~~~~~~~~~~~~~~~~~~~~~~~^
        m,
        ^^
    ...<2 lines>...
        **kwargs,
        ^^^^^^^^^
    )
    ^
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\langchain_core\language_models\chat_models.py", line 960, in _generate_with_cache
    result = self._generate(
        messages, stop=stop, run_manager=run_manager, **kwargs
    )
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\langchain_openai\chat_models\base.py", line 783, in _generate
    response = self.client.create(**payload)
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\openai\_utils\_utils.py", line 279, in wrapper
    return func(*args, **kwargs)
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\openai\resources\chat\completions\completions.py", line 929, in create
    return self._post(
           ~~~~~~~~~~^
        "/chat/completions",
        ^^^^^^^^^^^^^^^^^^^^
    ...<43 lines>...
        stream_cls=Stream[ChatCompletionChunk],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\openai\_base_client.py", line 1276, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))     
                           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^      
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\openai\_base_client.py", line 949, in request
    return self._request(
           ~~~~~~~~~~~~~^
        cast_to=cast_to,
        ^^^^^^^^^^^^^^^^
    ...<3 lines>...
        retries_taken=retries_taken,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\HO VAN ANH\AppData\Local\Programs\Python\Python313\Lib\site-packages\openai\_base_client.py", line 1057, in _request
    raise self._make_status_error_from_response(err.response) from None
openai.BadRequestError: Error code: 400 - {'error': {'message': "An assistant message with 'tool_calls' must be followed by tool messages responding to each 'tool_call_id'. The following tool_call_ids did not have response messages: call_WZJmK4VPpI5IkLUMFNNf3pED", 'type': 'invalid_request_error', 'param': 'messages.[2].role', 'code': None}}
During task with name 'agent' and id '0da5a267-1d20-5f67-45cb-1db57a2bfcb2'
```


## 2.1 Cải tiến
- Gợi ý cho tao ý tưởng cái tiến thêm project AI-Agent này
