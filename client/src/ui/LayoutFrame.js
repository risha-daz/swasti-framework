import { Breadcrumb, Layout, Menu } from "antd";
import { Recognizer } from "../recognizer";
const { Header, Content, Footer } = Layout;
const LayoutFrame = (props) => (
  <Layout className='layout'>
    <Header>
      <div className='logo'>
        {" "}
        <h1 style={{ color: "white" }}>SWASTi Framework</h1>
      </div>
      <Menu
        mode='horizontal'
        defaultSelectedKeys={["2"]}
        items={new Array(15).fill(null).map((_, index) => {
          const key = index + 1;
          return {
            key,
            label: `nav ${key}`,
          };
        })}
      />
    </Header>
    <Content
      style={{
        padding: "0 50px",
      }}
    >
      <p></p>
      <br />
      <div className='site-layout-content'>
        <Recognizer />
      </div>
    </Content>
    <Footer
      style={{
        textAlign: "center",
      }}
    >
      Ant Design ©2018 Created by Ant UED
    </Footer>
  </Layout>
);

export default LayoutFrame;
