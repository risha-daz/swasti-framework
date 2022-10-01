import Graphs from "./Graphs";
import { Space, Card } from "antd";
const DisplayFrame = (props) => {
  return (
    <>
      {/**{props.graphs && (
        <Space
          direction='vertical'
          size='middle'
          style={{
            display: "flex",
          }}
        >
          <Card title='Input Map' size='small'>
            <Graphs src={props.graphs.input_map} />
          </Card>
          <Card title='Solar Surface Map' size='small'>
            <Graphs src={props.graphs.solar_surface_map} />
          </Card>
          <Card title='Fieldlines' size='small'>
            <Graphs src={props.graphs.fieldlines} />
          </Card>
          <Card title='Solar Surface Map (Br vs Longitude)' size='small'>
            <Graphs src={props.graphs.solar_surface_magnetic_field} />
          </Card> 
          <Card title='Velocituy at 1AU' size='small'>
            <Graphs src={props.graphs.velocity_at_1AU} />
          </Card>

          <Card title='Comparison (Correlating)' size='small'>
            <Graphs src={props.graphs.comparison} />
          </Card>
          <Card title='Velocity with increasing R' size='small'>
            <Graphs src={props.graphs.vel_with_r} />
          </Card>
        </Space>
      )}*/}
    </>
  );
};

export default DisplayFrame;
