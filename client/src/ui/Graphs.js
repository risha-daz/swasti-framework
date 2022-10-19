import { Image } from "antd";

const Graphs = (props) => {
  return (
    <>
      {props.src && (
        <Image.PreviewGroup>
          <Image width={600} src={props.src} />
        </Image.PreviewGroup>
      )}
    </>
  );
};

export default Graphs;
