import { Button} from "antd";
import React, { useState, useEffect } from "react";
import styled from "styled-components";

const Wrapper = styled.div`
  display: flex;
  justify-content: center;
`;

const StyledButton = styled(Button)`
  box-sizing: border-box;
  margin-left: 0.5rem;
`;
interface Props {
  onModelChange: (value: string) => void;
  onModelSelect: (value: string) => void;
  loading: boolean;
}

export const models: Array<{ name: string; path: string }> = [
  
  {
    name: "Indian English",
    path: "vosk-model-small-en-in-0.4.tar.gz",
  },
  {
    name: "English",
    path: "vosk-model-small-en-us-0.15.tar.gz",
  },
];

const ModelLoader: React.FunctionComponent<Props> = ({
  onModelSelect,
  loading,
}) => {
  const [model, setModel] = useState(models[0].path);
  useEffect(() => {
    onModelSelect(model)
  }, [])
  
  return (
    <Wrapper>
      <span>
        {loading ? "Please wait while Loading" : "Click on Speak to Start Speaking"}
      </span>
    </Wrapper>
  );
};

export default ModelLoader;
