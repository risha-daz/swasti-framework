import { Button, Modal, Slider } from "antd";
import { useState } from "react";
import { SettingOutlined } from "@ant-design/icons";
const ChartSettings = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const showModal = () => {
    setIsModalOpen(true);
  };
  const handleOk = () => {
    setIsModalOpen(false);
  };
  const handleCancel = () => {
    setIsModalOpen(false);
  };
  const onChange = (value) => {
    console.log("onChange: ", value);
  };
  const onAfterChange = (value) => {
    console.log("onAfterChange: ", value);
  };
  return (
    <>
      <Button icon={<SettingOutlined />} onClick={showModal} size='small'>
        Chart Settings
      </Button>
      <Modal
        title='Chart Settings'
        visible={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        Temperature range:
        <Slider
          step={1}
          min={0}
          max={10}
          defaultValue={6}
          onChange={onChange}
          onAfterChange={onAfterChange}
        />
        Velocity Range:
        <Slider
          range
          min={0}
          max={1000}
          step={100}
          defaultValue={[200, 800]}
          onChange={onChange}
          onAfterChange={onAfterChange}
        />
        Density Range:
        <Slider
          range
          step={1}
          min={0}
          max={14}
          defaultValue={[0, 10]}
          onChange={onChange}
          onAfterChange={onAfterChange}
        />
      </Modal>
    </>
  );
};
export default ChartSettings;
