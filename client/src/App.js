import wordsToNumbers from "words-to-numbers";
import { useState, useEffect } from "react";
import { Button, Space, Collapse } from "antd";
import { DeleteOutlined } from "@ant-design/icons";
import DisplayFrame from "./ui/DisplayFrame";
import ManualInput from "./ui/ManualInput";
import AudioPlayer from "./ui/AudioPlayer";

const { Panel } = Collapse;

function App(props) {
  const [graphs, setGraphs] = useState({});
  const [quer, setQuer] = useState("");
  const [show, setShow] = useState(false);
  useEffect(() => {
    let final = "";
    props.utterances.forEach((ele) => {
      final =
        final +
        "+" +
        wordsToNumbers(ele.text, { impliedHundreds: true })
          .toString()
          .split(" ")
          .join("");
    });
    console.log(final);
    setQuer(final);
  }, [props, props.utterances]);

  const fetchData = async () => {
    console.log(`https://spacewapi.herokuapp.com/?text=${quer}`);
    const res = await fetch(`https://spacewapi.herokuapp.com/?text=${quer}`);
    const data = await res.json();
    console.log(data);
    setGraphs(data);
  };

  const fetchVelData = async () => {
    console.log(`https://spacewapi.herokuapp.com/avgvelocity/?text=${quer}`);
    const res = await fetch(
      `https://spacewapi.herokuapp.com/avgvelocity/?text=${quer}`
    );
    const data = await res.json();
    console.log(data);
    setGraphs(data);
    setShow(true);
  };

  const manualInp = (query) => {
    console.log(query);
    query && setQuer(query.split("/").join("+"));
  };

  return (
    <Space
      direction='vertical'
      size='middle'
      style={{
        display: "flex",
        textAlign: "center",
      }}
      className='panel'
    >
      <h4>OR</h4>
      <Collapse defaultActiveKey={["0"]}>
        <Panel header='Manual Input' key='1'>
          <ManualInput manualInp={manualInp} />
        </Panel>
      </Collapse>

      <Space size='small'>
        <Button type='primary' onClick={() => fetchVelData()}>
          Get Graphs
        </Button>
        <Button
          icon={<DeleteOutlined />}
          type='primary'
          danger
          onClick={props.clearVoice}
          color='#1E3388'
        >
          Clear
        </Button>
      </Space>
      {show && (
        <AudioPlayer date={graphs.date} vel={graphs.val} url={graphs.url} />
      )}
      <DisplayFrame graphs={graphs} />
    </Space>
  );
}

export default App;
