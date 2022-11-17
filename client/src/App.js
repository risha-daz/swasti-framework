import wordsToNumbers from "words-to-numbers";
import { useState, useEffect } from "react";
import { Button, Space, Collapse } from "antd";
import { DeleteOutlined } from "@ant-design/icons";
import DisplayFrame from "./ui/DisplayFrame";
import ManualInput from "./ui/ManualInput";

const { Panel } = Collapse;

function App(props) {
  const [graphs, setGraphs] = useState({});
  const [graphdata, setGraphdata] = useState({});
  const [quer, setQuer] = useState("");
  const [show, setShow] = useState(true);
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

  const fetchData = async () => {};

  const fetchVelData = async () => {
    let tempurl = `swasti-framework.azurewebsites.net//?text=${quer}`;
    const res = await fetch("https://" + tempurl);
    const data = await res.json();
    setGraphs(data);
    setShow(true);
    const res2 = await fetch(
      `https://swasti-framework.azurewebsites.net/get_obs?param=${quer}`
    );
    const data2 = await res2.json();
    setGraphdata(data2);
  };

  const manualInp = (query) => {
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

      <DisplayFrame graphs={graphs} show={show} graphdata={graphdata} />
    </Space>
  );
}

export default App;
