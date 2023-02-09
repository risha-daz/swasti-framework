import { Breadcrumb, Layout, Menu, Button, PageHeader } from "antd";
import { Recognizer } from "../recognizer";
const { Header, Content, Footer } = Layout;

const LayoutFrame = (props) => {
  const dayNames = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursdsay",
    "Friday",
    "Saturday",
  ];
  const month = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  var today = new Date(),
    date =
      month[today.getMonth()] +
      "  " +
      today.getDay() +
      ", " +
      today.getFullYear();
  return (
    <Layout className='layout'>
      <PageHeader
        ghost={false}
        className='site-page-header'
        title={
          <span>
            <span
              style={{
                fontSize: "25px",
                color: "white",
                paddingBottom: "0",
                marginBottom: "0",
              }}
            >
              SWASTi Framework{" "}
            </span>

            <span style={{ color: "#d9d9d9", fontSize: "15px" }}>
              for space weather prediction
            </span>
          </span>
        }
        extra={[
          <div
            style={{
              textAlign: "right",
              color: "white",
              padding: "0px",
              margin: "0px",
            }}
          >
            <span style={{ fontSize: "20px" }}>{dayNames[today.getDay()]}</span>
            <h5 style={{ color: "white" }}>{date}</h5>
          </div>,
        ]}
      />
      {/* <Header>
        <div>
          <h1 style={{ color: "white" }}>SWASTi Framework</h1>
        </div>
      </Header> */}
      <Layout>
        <Content
          style={{
            padding: "0 50px",
          }}
        >
          {/* <div className='site-layout-content'>
      <DateWidget />
    </div> */}
          <br />
          <div className='site-layout-content'>
            <Recognizer />
          </div>
        </Content>
      </Layout>
      <Footer
        style={{
          textAlign: "center",
        }}
      >
        Footnote ©2022 Footnote
      </Footer>
    </Layout>
  );
};

export default LayoutFrame;
