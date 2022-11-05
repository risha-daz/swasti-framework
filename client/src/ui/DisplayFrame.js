import { Tabs, Row, Col, Divider, Tag } from "antd";
import { Fragment } from "react";
import { CheckCircleFilled } from "@ant-design/icons";
import Graph from "./Graph";
import AudioPlayer from "./AudioPlayer";

const DisplayFrame = (props) => {
  return (
    <Fragment>
      <Divider orientation='left'>Today's Weather</Divider> <br></br>
      <Row>
        <Col span={10}>
          <Row>
            {" "}
            <Col span={9}>
              <CheckCircleFilled
                style={{ color: "#097969", fontSize: "3rem" }}
              />
              <p></p>
              <Tag icon={<CheckCircleFilled />} color='success'>
                safe
              </Tag>
            </Col>
            <Col span={9}>
              Temperature: 37 C <br></br> Density: 37 <br></br> Solar Wind Speed
              300 km/hr
            </Col>
          </Row>
        </Col>
        <Col span={14}>
          {props.show && (
            <AudioPlayer
              date={props.graphs.date}
              vel={props.graphs.val}
              url={props.graphs.url}
            />
          )}
        </Col>
      </Row>
      <Tabs defaultActiveKey='1'>
        <Tabs.TabPane tab='Temperature' key='1'>
          <Graph />
        </Tabs.TabPane>
        <Tabs.TabPane tab='Velocity' key='2'>
          <Graph />
        </Tabs.TabPane>
        <Tabs.TabPane tab='Density' key='3'>
          <Graph type='line' />
        </Tabs.TabPane>
      </Tabs>
    </Fragment>
  );
};

export default DisplayFrame;
