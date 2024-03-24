import React, { useState } from "react";
import { CohereClient } from "cohere-ai";

import "./App.css";

import Message from "./components/Message";
import Input from "./components/Input";
import History from "./components/History";
import Clear from "./components/Clear";
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UploadOutlined,
  UserOutlined,
  VideoCameraOutlined,
} from '@ant-design/icons';
import { Layout, Menu, Button, theme } from 'antd';

export default function App() {
  const { Header, Sider, Content } = Layout;
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const cohere = new CohereClient({
    token: process.env.REACT_APP_COHERE_API_KEY,
  });
  const [collapsed, setCollapsed] = useState(false);
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

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
  };  

  const clear = () => {
    setMessages([]);
    setHistory([]);
  };

  return (
      <Layout>
      <Sider trigger={null} collapsible collapsed={collapsed}>
        <div className="demo-logo-vertical" />
        <Menu
          theme="dark"
          mode="inline"
          defaultSelectedKeys={['1']}
          items={[
            {
              key: '1',
              icon: <UserOutlined />,
              label: 'nav 1',
            },
            {
              key: '2',
              icon: <VideoCameraOutlined />,
              label: 'nav 2',
            },
            {
              key: '3',
              icon: <UploadOutlined />,
              label: 'nav 3',
            },
          ]}
        />
      </Sider>
      <Layout>
        <Header
          style={{
            padding: 0,
            background: colorBgContainer,
          }}
        >
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{
              fontSize: '16px',
              width: 64,
              height: 64,
            }}
          />
        </Header>
        <Content
          style={{
            margin: '24px 16px',
            padding: 24,
            width: 'auto',
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
          }}
        >
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
            {/* <div className="Column">
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
            </div> */}
          </div>
        </Content>
      </Layout>
    </Layout>
  );
}
