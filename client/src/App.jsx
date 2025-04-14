import "./App.css";
import Header from "./components/Header/Header";
import Form from "./components/Form/Form";
import { useState } from "react";
import Description from "./components/Description/Description";

export default function App() {
  const [response, setResponse] = useState({});
  return (
    <div className="main">
      <Header />
      {response.name ? (
        <Description
          name={response.name}
          description={response.description}
          setResponse={setResponse}
        />
      ) : (
        <Form setResponse={setResponse} />
      )}
    </div>
  );
}
