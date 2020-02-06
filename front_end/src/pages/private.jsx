import React, {Component} from 'react';
//import './App.css';
import Sidebar from './components/sidebar'
import Loading from './components/loading'
import BigMessage from './components/succes'
import FormAddMoney from "./components/formAddMoney";
import FormTransaction from "./components/formTransaction";
import FormDebit from "./components/formDebit";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";

class Private extends Component {
    render() {
        if (false && this.props.getAuth() === "") {
            return (
                <div className={"overlay popup"}>
                    <h1>404</h1>
                    <h4>NOT FOUND</h4>
                </div>
            )
        }
        return (
            <>
                <div>
                    <Loading loading={this.props.loading}/>
                    <BigMessage small_text={this.props.big_msg_small_text}
                                icon={this.props.big_msg_icon}
                                text={this.props.big_msg_text}
                                show={this.props.big_msg}/>
                    <Sidebar getAuth={this.props.getAuth} toggleLoading={this.props.toggleLoading}
                             toggleBigMessage={this.props.toggleBigMessage}/>
                </div>
                <Container>
                    <Row className="show-grid">
                        <Col sm={12} md={8}>
                            <FormAddMoney/>
                        </Col>
                        <Col sm={12} md={4}>
                            <FormTransaction/>
                        </Col>
                        <Col sm={12} md={4}>
                            <FormDebit/>
                        </Col>
                    </Row>

                </Container>

            </>

        );
    }
}


export default Private;
