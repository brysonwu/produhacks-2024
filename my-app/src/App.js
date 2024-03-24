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
    token: "4fO1Ufhr0lgREDz0XBKs4C8QKQbUEu0vvbsAhtt6",
  });

  const handleSubmit = async () => {
    const prompt = {
      role: "user",
      content: input,
    };
  
    // Update messages state optimistically
    setMessages([...messages, prompt]);

    (async () => {
      const prediction = await cohere.generate({
          prompt: input,
          maxTokens: 10,
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
  
    // try {
    //   // const response = await fetch("https://api.openai.com/v1/chat/completions", {
    //   //   method: "POST",
    //   //   headers: {
    //   //     Authorization: `Bearer ${process.env.REACT_APP_OPENAI_API_KEY}`,
    //   //     "Content-Type": "application/json",
    //   //   },
    //   //   body: JSON.stringify({
    //   //     model: "gpt-3.5-turbo",
    //   //     messages: [...messages, prompt],
    //   //   }),
    //   // });
  
    //   const data = await response.json();
    //   const res = data.choices[0].message.content;
  
    //   // Use the updated messages state after API response
    //   setMessages((prevMessages) => [
    //     ...prevMessages,
    //     {
    //       role: "assistant",
    //       content: res,
    //     },
    //   ]);
  
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