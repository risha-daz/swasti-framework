import { InputNumber, DatePicker, Radio } from "antd";
import { useState } from "react";

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
    </>
  );
};

export default Graphs;
