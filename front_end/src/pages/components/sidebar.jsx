import React, {Component} from 'react'
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Button from "react-bootstrap/Button";
import Image from 'react-bootstrap/Image';
import ModalSignUp from './modalSignUp'
import ModalLogin from './modalLogin'
import {withRouter} from 'react-router-dom';

class Sidebar extends Component {
    render() {
        return (
            <Navbar expand="lg">
                <Navbar.Brand>
                    <Image src={process.env.PUBLIC_URL + "/images/2.png"} style={{width: "100px"}}/>
                </Navbar.Brand>
                <Navbar.Toggle/>
                <div hidden={this.props.home}>
                    <Navbar.Collapse>
                        <Nav className="text-center text-right">
                            <h1><Button variant="outline-dark" size="lg" onClick={()=>{this.props.history.push("/");}}>Logout</Button></h1>
                        </Nav>
                    </Navbar.Collapse>
                </div>
                <Navbar.Collapse>
                    <Nav className="justify-content-end" style={{width: "100%"}}>
                        <div hidden={!this.props.home}>
                        <ModalLogin
                            toggleLoading={this.props.toggleLoading}
                            toggleBigMessage={this.props.toggleBigMessage}
                            addAdmin={this.props.home}
                            setAuth={this.props.setAuth}


                        />
                        </div>
                        <ModalSignUp
                            toggleLoading={this.props.toggleLoading}
                            toggleBigMessage={this.props.toggleBigMessage}
                            getAuth={this.props.getAuth}
                            addAdmin={this.props.home}
                        />
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        )
            ;

    }
}
export  default withRouter(Sidebar);