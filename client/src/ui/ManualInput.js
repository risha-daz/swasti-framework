import {
  InputNumber,
  DatePicker,
  Divider,
  Radio,
  Row,
  Col,
  Switch,
  Checkbox,
} from "antd";
import { useState } from "react";
const onChange = (checkedValues) => {
  console.log("checked = ", checkedValues);
};
const Graphs = (props) => {
  let month = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
  ];
  const [type, setType] = useState(1);
  const onselect = (ele) => {
    setType(ele.target.value);
  };
  const onSet = (ele, elestring) => {
    console.log(elestring || ele);
    if (elestring) {
      elestring =
        elestring.slice(0, 3) +
        month[parseInt(elestring.slice(3, 5)) - 1] +
        elestring.slice(5);
    }
    props.manualInp(elestring || ele);
  };
  return (
    <>
      <Radio.Group name='radiogroup' defaultValue={type}>
        <Radio value={1} onChange={onselect}>
          Date
        </Radio>
        <Radio value={2} onChange={onselect}>
          CR Number
        </Radio>
      </Radio.Group>
      {type === 1 ? (
        <DatePicker onChange={onSet} format={"DD/MM/YYYY"} />
      ) : (
        <InputNumber min={1905} max={2255} onChange={onSet} />
      )}
      <Divider orientation='center'>Select Plasma Properties</Divider>
      <Switch defaultChecked onChange={onChange} /> Show Graphs
      <Checkbox.Group
        style={{
          width: "100%",
        }}
        onChange={onChange}
      >
        <Row>
          <Col span={8}>
            <Checkbox value='A'>Flow Speed</Checkbox>
          </Col>
          <Col span={8}>
            <Checkbox value='B'>Proton Temperature</Checkbox>
          </Col>
          <Col span={8}>
            <Checkbox value='C'>Proton Density</Checkbox>
          </Col>
          <Col span={8}>
            <Checkbox value='D'>Magnetic Field</Checkbox>
          </Col>
          <Col span={8}>
            <Checkbox value='E'>Flow Pressure</Checkbox>
          </Col>
        </Row>
      </Checkbox.Group>
    </>
  );
};

export default Graphs;
