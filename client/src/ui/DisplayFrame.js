import { Tabs, Row, Col, Divider, Tooltip, Button, Badge } from "antd";
import { Fragment } from "react";
import Weekday from "./Weekday";
import { RightOutlined, LeftOutlined } from "@ant-design/icons";
import {
  CloseCircleFilled,
  ExclamationCircleFilled,
  CheckCircleFilled,
  SettingOutlined,
} from "@ant-design/icons";
import Graph from "./Graph";
import AudioPlayer from "./AudioPlayer";
const operations = (
  <Button icon={<SettingOutlined />} size='small'>
    Chart Settings
  </Button>
);
const DisplayFrame = (props) => {
  console.log(Object.keys(props.graphdata).length);
  return (
    <Fragment>
      <Divider orientation='left'>Weather Alerts</Divider>
      <Row>
        <Col span={12}>
          <div
            color='moderate'
            style={{
              backgroundColor: "#f6f6f6",
              borderRadius: "50px",
              padding: "0.9rem",
              paddingTop: "1.1rem",
              paddingRight: "0rem",
              margin: "0.9rem",
            }}
          >
            <Row>
              {" "}
              <Col span={8}>
                {props.graphs.val && (
                  <Fragment>
                    {parseFloat(props.graphs.val.split("k")) > 600 ? (
                      <Badge
                        style={{ backgroundColor: "#880808" }}
                        count={"severe"}
                      >
                        <CloseCircleFilled
                          style={{ color: "#DC143C", fontSize: "3rem" }}
                        />
                      </Badge>
                    ) : parseFloat(props.graphs.val.split("k")) > 400 ? (
                      <Badge
                        style={{ backgroundColor: "#FFBF00" }}
                        count={"alert"}
                      >
                        <ExclamationCircleFilled
                          style={{ color: "#E49B0F", fontSize: "3rem" }}
                        />
                      </Badge>
                    ) : (
                      <Badge
                        style={{ backgroundColor: "#4CBB17" }}
                        count={"safe"}
                      >
                        <CheckCircleFilled
                          style={{ color: "#097969", fontSize: "3rem" }}
                        />
                      </Badge>
                    )}
                  </Fragment>
                )}

                <p></p>
              </Col>
              <Col span={10} style={{ textAlign: "left" }}>
                Temperature:{" "}
                <b>{Math.round(props.graphs.avg_temp / 1e4) / 100} MK </b>
                <br></br> Density:{" "}
                <b>{Math.round(props.graphs.avg_den * 100) / 100} n/cc</b>
                <br></br> Speed: <b>{props.graphs.val}</b>
              </Col>{" "}
            </Row>{" "}
          </div>
        </Col>
        <Col span={12}>
          {props.show && (
            <AudioPlayer
              date={props.graphs.date}
              vel={props.graphs.val}
              url={props.graphs.url}
            />
          )}
        </Col>
      </Row>
      {Object.keys(props.graphdata).length !== 0 && (
        <Tabs tabBarExtraContent={operations} defaultActiveKey='1'>
          <Tabs.TabPane tab='Temperature' key='1'>
            <Graph
              type='bar'
              data={props.graphdata.temp}
              title='Temperature (MK)'
              label='temp'
            />
          </Tabs.TabPane>
          <Tabs.TabPane tab='Velocity' key='2'>
            <Graph
              type='line'
              data={props.graphdata.velocity}
              data2={props.graphdata.calcvel}
              title='Wind Speed (km/s)'
              label='vel'
            />
          </Tabs.TabPane>
          <Tabs.TabPane tab='Density' key='3'>
            <Graph
              type='line'
              data={props.graphdata.density}
              title='Density (n/cc)'
              label='dens'
            />
          </Tabs.TabPane>
        </Tabs>
      )}
      <Divider orientation='left'>This Week</Divider>
      <Row justify='center' gutter={8} align='middle'>
        <Col span={1}>
          <Tooltip title='Previous Week'>
            <Button type='text' shape='circle' icon={<LeftOutlined />} />
          </Tooltip>
        </Col>
        {props.weekly &&
          props.weekly.map((item, ind) => (
            <Weekday data={item} ind={ind === 0} key={ind} />
          ))}
        <Col span={1}>
          <Tooltip title='Next Week'>
            <Button type='text' shape='circle' icon={<RightOutlined />} />
          </Tooltip>
        </Col>
      </Row>
    </Fragment>
  );
};

DisplayFrame.defaultProps = {
  graphdata: {
    temp: [
      256031, 254548, 301362, 213076, 202391, 188560, 182158, 140751, 138451,
      125780, 123067, 120155, 105004, 9999999, 63296, 66112, 104670, 139632,
      135436, 124822, 99517, 89187, 76672, 76558, 65430, 70923, 62905, 112596,
      450530, 263192, 426853, 434324, 154341, 173847, 172816, 56683, 121476,
      134847, 243691, 265442, 315931, 305047, 283811, 270334, 383326, 372681,
      407739, 393890,
    ],
  },
  graphs: {
    val: "509.33km/s",
  },
};
export default DisplayFrame;
