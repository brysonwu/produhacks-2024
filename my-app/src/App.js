import { useState } from "react";
import { CohereClient } from "cohere-ai";

import Message from "./components/Message";
import Input from "./components/Input";
import History from "./components/History";
import Clear from "./components/Clear";

import "./App.css";

export default function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const cohere = new CohereClient({
    token: process.env.REACT_APP_COHERE_API_KEY,
  });

  const handleSubmit = async () => {
    const prompt = {
      role: "user",
      content: input,
    };
  
    setMessages([...messages, prompt]);

    (async () => {
      const prediction = await cohere.generate({
          prompt: input,
          // maxTokens: 50,
      });
      
      console.log("Received prediction", prediction);
      const data = await prediction;
      const res = data.generations[0].text;
  
      // Use the updated messages state after API response
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          role: "assistant",
          content: res,
        },
      ]);
  
      setHistory((prevHistory) => [...prevHistory, { question: input, answer: res }]);
      setInput("");
    })();
  
    

    //   setHistory((prevHistory) => [...prevHistory, { question: input, answer: res }]);
    //   setInput("");
    // } catch (error) {
    //   console.error("Error:", error);
    //   // Handle error
    // }
  };  

  const clear = () => {
    setMessages([]);
    setHistory([]);
  };

  return (
    <div className="App">
      <div className="Column">
        <h3 className="Title">Chat Messages</h3>
        <div className="Content">
          {messages.map((el, i) => {
            return <Message key={i} role={el.role} content={el.content} />;
          })}
        </div>
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onClick={input ? handleSubmit : undefined}
        />
      </div>
      <div className="Column">
        <h3 className="Title">History</h3>
        <div className="Content">
          {history.map((el, i) => {
            return (
              <History
                key={i}
                question={el.question}
                onClick={() =>
                  setMessages([
                    { role: "user", content: history[i].question },
                    { role: "assistant", content: history[i].answer },
                  ])
                }
              />
            );
          })}
        </div>
        <Clear onClick={clear} />
      </div>
    </div>
  );
}
