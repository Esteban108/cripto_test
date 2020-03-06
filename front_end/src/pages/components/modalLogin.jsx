import React, {Component} from 'react'
import Modal from 'react-bootstrap/Modal'
import Button from "react-bootstrap/Button";
import Form from 'react-bootstrap/Form';
import {withRouter} from 'react-router-dom';

class ModalLogin extends Component {
    constructor(props, context) {
        super(props, context);

        this.handleShow = this.handleShow.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.login = this.login.bind(this);
        this.handleInput = this.handleInput.bind(this);
        this.state = {
            show: false,
            email: "",
            password: ""
        };
    }


    handleClose() {
        this.setState({show: false});
    }

    handleShow() {
        this.setState({show: true});
        //updateShow(true)
    }

    handleInput(event) {
        this.setState({[event.target.name]: event.target.value})
    }

    end_login(obj) {
        this.props.toggleLoading();
        if (obj.status === 200) {
            this.handleClose();
            this.props.setAuth(obj.body.token_type + " " +obj.body.access_token);
            this.props.history.push("/private")

        }
        if (obj.status !== 200) {
            this.props.toggleBigMessage("Fallido!", "icon-circle-cross", "TODO: añadir msg error");

        }
    }


    login() {
        this.props.toggleLoading();

        let details = {
            "grant_type": '',
            'username': this.state.email,
            'password': this.state.password,
            "scope": '',
            "client_id": '',
            "client_secret": ''
        };

        let formBody = [];
        for (let property in details) {
            let encodedKey = encodeURIComponent(property);
            let encodedValue = encodeURIComponent(details[property]);
            formBody.push(encodedKey + "=" + encodedValue);
        }
        formBody = formBody.join("&");

        fetch("http://localhost:8100/token", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                "accept": "application/json"
            },
            body: formBody
        }).then(r => r.json().then(data => ({status: r.status, body: data})))
            .then(obj => this.end_login(obj));

    }

    render() {

        return (
            <>
                <h1><Button variant="outline-light" size="lg" onClick={this.handleShow}>LogIn</Button></h1>

                <Modal
                    show={this.state.show} onHide={this.handleClose}
                    size="lg"
                    aria-labelledby="contained-modal-title-vcenter"
                    centered
                >
                    <Modal.Header closeButton>
                        <Modal.Title id="contained-modal-title-vcenter">
                            Registrarse
                        </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form>
                            <Form.Group controlId="SignUp.email">
                                <Form.Label>Correo</Form.Label>
                                <Form.Control value={this.state.email}
                                              name="email" type="email" placeholder="name@example.com"
                                              onChange={this.handleInput}/>
                            </Form.Group>
                            <Form.Group controlId="SignUp.password">
                                <Form.Label>Contraseña</Form.Label>
                                <Form.Control name="password" value={this.state.password} type="password"
                                              placeholder="contraseña"
                                              onChange={this.handleInput}/>
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={this.handleClose}>
                            Cerrar
                        </Button>
                        <Button variant="primary" onClick={this.login}>
                            Entrar
                        </Button>
                    </Modal.Footer>
                </Modal>
            </>
        );
    }
}

export default withRouter(ModalLogin);