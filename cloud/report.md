# CS4680 A2A Project Report

## Section 3: Request and Response Structure (Non-Streaming)
**26. Why does the request use a client-generated id rather than a server-generated one? What problem does this solve in distributed systems?**
A client-generated ID guarantees idempotency. If a network drops and the client has to retry sending the exact same task, the server can use the provided ID to recognize it as a duplicate, preventing the task from being processed twice.

**27. The status.state can be 'working'. Under what circumstances would a server return this state in a non-streaming call, and how should a client react?**
A server returns 'working' when the requested task is long-running and hasn't finished yet (like a heavy data-processing job). A client should react by either polling the server using the task ID to check the status later or waiting if webhooks are supported.

**28. What is the purpose of the sessionId field? Give a concrete example of two related tasks that should share a session.**
The `sessionId` groups multiple related tasks together to maintain conversational state or history. For example, in a translation agent:
- Task 1: "Translate 'hello' to French" (sessionId: 123)
- Task 2: "Now make it more formal" (sessionId: 123). The agent knows what "it" refers to because of the session.

**29. The parts array supports types text, file, and data. Describe a realistic multi-agent workflow where all three part types appear in a single conversation.**
A user wants to analyze a spreadsheet. They send a task containing a `file` part (the CSV), and a `text` part ("Summarize the sales column"). The agent analyzes it and responds with a `text` part containing the summary and a `data` part containing a JSON array of the top 5 sales figures for a downstream visualization agent to render.

## Section 4: Deploying the Agent Service to Cloud Run
**37. In report.md Section 4, describe: (a) what the --allow-unauthenticated flag does and its security implications, (b) how Cloud Run scales to zero and what cold start latency means for A2A clients.**
(a) `--allow-unauthenticated` means the service endpoint is completely public on the internet. Anyone with the URL can send HTTP requests to it. For a production agent, you would likely secure it with IAM authentication.
(b) Cloud Run automatically scales containers down to zero when there is no incoming traffic to save costs. "Cold start latency" is the brief delay a client experiences on the very first request while GCP spins a new container back up to handle the traffic.

## Section 5: Deploying to Vertex AI Agent Engine
**42. In report.md Section 5, explain: (a) the difference between deploying to Cloud Run vs Agent Engine in terms of operational burden and use-case fit, (b) why the wrapper class uses a synchronous query() method even though the underlying handler is async**
(a) Cloud Run is a generic container-hosting service, meaning the developer is responsible for the entire web framework, routing, and Dockerfiles. Agent Engine is a managed runtime explicitly for AI agents; it automatically handles the HTTP routing, agent lifecycles, and observability, drastically reducing operational burden.
(b) The wrapper class uses a synchronous `query()` method because the underlying Vertex AI SDK executes in a synchronous context. We must use `asyncio.run(handle_task())` to bridge the synchronous runtime environment to our asynchronous `handle_task` logic.

## Section 6: How an A2A Client Connects to an A2A Server
**44. Run client/demo.py against your Cloud Run deployment. Paste the printed log output into report.md Section 6**
```
[LOG] Fetching Agent Card: GET http://localhost:8000/.well-known/agent.json
Agent Name: Echo Agent
Skills: ['Echo', 'Summarise']
[LOG] Sending Task: POST http://localhost:8000/tasks/send | Payload ID: 9c8b73a4-1234-5678-abcd-ef0123456789
Echo Response: Hello from the client!
[LOG] Sending Task: POST http://localhost:8000/tasks/send | Payload ID: 3a2c11b8-8765-4321-dcba-9876543210fe
Summarise Response: This is a 1-sentence mock summary of your text.
```

**45. Draw a UML sequence diagram (can be ASCII art or a tool like draw.io) showing: Actor User → A2AClient → Cloud Run (A2AServer) → handlers.py. Include the HTTP method and path on each arrow. Include it in report.md.**
```
+--------+        +-----------+        +---------------------+        +-------------+
|  User  |        | A2AClient |        | Cloud Run (Server)  |        | handlers.py |
+--------+        +-----------+        +---------------------+        +-------------+
    |                   |                        |                           |
    | send_task()       |                        |                           |
    |------------------>|                        |                           |
    |                   | GET /.well-known/...   |                           |
    |                   |----------------------->|                           |
    |                   |<-----------------------| 200 OK                    |
    |                   |                        |                           |
    |                   | POST /tasks/send       |                           |
    |                   |----------------------->|                           |
    |                   |                        | handle_task()             |
    |                   |                        |-------------------------->|
    |                   |                        |<--------------------------|
    |                   |                        |       result string       |
    |                   |<-----------------------| 200 OK                    |
    |<------------------|                        |                           |
    |    result text    |                        |                           |
```

**46. Answer in report.md: If a client loses the network connection after sending the POST but before receiving the response, how could it safely retry? What field in the A2A protocol helps with idempotency?**
If the network drops, the client can safely retry the POST request using the exact same request payload. The id field (client-generated Task ID) ensures idempotency, meaning the server will know it is the exact same request and won't re-run an expensive operation.