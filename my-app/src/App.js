import "./App.css";
import ChatForm from "./Components/ChatForm";
import Header from "./Components/Header";
import Answers from "./Components/Answers";
import React, { useState } from 'react';

const App = () => {
  const [messages, setMessages] = useState([]);

  const responseGenerate = async (inputText, setInputText) => {
  };

  return (
    <div className="App">
      <Header />
      <ChatForm responseGenerate={responseGenerate} />
      <Answers messages={messages} />
    </div>
  );
};

export default App;