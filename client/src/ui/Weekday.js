import { Card, Col, Tag, Button, Badge } from "antd";
import { Fragment } from "react";
import {
  CloseCircleFilled,
  ExclamationCircleFilled,
  CheckCircleFilled,
  SettingOutlined,
} from "@ant-design/icons";
const { Meta } = Card;
const Weekday = (props) => {
  return (
    <Col span={props.ind ? 4 : 3}>
      <Card
        hoverable='true'
        size={props.ind ? "default" : "small"}
        title={props.data[0].substr(5, 6)}
      >
        <h1>
          {props.data[2] && (
            <Fragment>
              {parseFloat(props.data[2]) > 600 ? (
                <CloseCircleFilled
                  style={{
                    color: "#DC143C",
                    fontSize: props.ind ? "2.5rem" : "2rem",
                  }}
                />
              ) : parseFloat(props.data[2]) > 400 ? (
                <ExclamationCircleFilled
                  style={{
                    color: "#E49B0F",
                    fontSize: props.ind ? "2.5rem" : "2rem",
                  }}
                />
              ) : (
                <CheckCircleFilled
                  style={{
                    color: "#097969",
                    fontSize: props.ind ? "2.5rem" : "2rem",
                  }}
                />
              )}
            </Fragment>
          )}
          <Tag color='blue'>{Math.round(props.data[1] / 1e4) / 100} MK</Tag>
          <Tag color='cyan'>{Math.round(props.data[2])} km/s</Tag>
          <Tag color='purple'>{props.data[3]} n/cc</Tag>
        </h1>
      </Card>
    </Col>
  );
};

export default Weekday;
