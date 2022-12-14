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

const options = [
  { label: "Flow Speed", value: "velocity" },
  { label: "Proton Temperature", value: "temp" },
  { label: "Proton Density", value: "density" },
  /*{ label: "Magnetic Field", value: "mag" },
  { label: "Flow Pressure", value: "pres" },*/
];

const ManualInput = (props) => {
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
  const onChange = () => {
    props.setShowGraphs(!props.showGraphs);
  };
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
        {/* <Radio value={2} onChange={onselect}>
          CR Number
        </Radio> */}
      </Radio.Group>
      {type === 1 ? (
        <DatePicker onChange={onSet} format={"DD/MM/YYYY"} />
      ) : (
        <InputNumber min={1905} max={2255} onChange={onSet} />
      )}
      <Divider orientation='center'>Select Plasma Properties</Divider>
      <Switch
        defaultChecked
        onChange={onChange}
        value={props.setShowGraphs}
      />{" "}
      Show Graphs{" "}
      <Switch defaultChecked onChange={onChange} value={props.setShowGraphs} />{" "}
      Show Weekly data<br></br>
      <Checkbox.Group
        options={options}
        defaultValue={["velocity", "temp", "density"]}
        onChange={onChange}
      />
      <br />
    </>
  );
};

export default ManualInput;
