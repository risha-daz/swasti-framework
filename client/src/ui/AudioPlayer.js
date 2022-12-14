import { Button } from "antd";
import ReactAudioPlayer from "react-audio-player";
import { SoundOutlined, SoundFilled } from "@ant-design/icons";
import { useEffect, useState } from "react";

const useAudio = (url) => {
  const [audio, setAudio] = useState(new Audio(url));
  const [playing, setPlaying] = useState(true);
  const toggle = () => setPlaying(!playing);

  useEffect(() => {
    setAudio(new Audio(url));
    setPlaying(true);
  }, [url]);

  useEffect(() => {
    playing ? audio.play() : audio.pause();
    audio.currentTime = 0;
  }, [playing]);

  useEffect(() => {
    audio.addEventListener("ended", () => setPlaying(false));
    return () => {
      audio.removeEventListener("ended", () => setPlaying(false));
    };
  }, [audio]);

  return [playing, toggle];
};

const AudioPlayer = (props) => {
  const [playing, toggle] = useAudio(props.url);
  useEffect(() => {
    toggle();
  }, []);

  return (
    <div>
      <Button
        type={playing ? "text" : "default"}
        shape='circle'
        icon={playing ? <SoundFilled /> : <SoundOutlined />}
        onClick={toggle}
        size='large'
      />
      <br></br>
      <h2>
        Average velocity on{" "}
        {props.date ? props.date.split("+").join(" ") : "NaN"} is{" "}
        {props.vel ? props.vel : "NaN"}
      </h2>
    </div>
  ); /*
  return (
    <>
      <Button type='primary' icon={<SoundOutlined />} />
      <ReactAudioPlayer
        src='https://spacewapi.herokuapp.com/avgvelocity/?text=11+january+twentytwenty'
        autoPlay={true}
      />
    </>
  );*/
};

export default AudioPlayer;
