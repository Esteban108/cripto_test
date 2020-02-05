import React, {Component} from 'react'
import Modal from 'react-bootstrap/Modal'
import Button from "react-bootstrap/Button";
import Form from 'react-bootstrap/Form';
//import ReactBootstrapStyle from "react-bootstrap.react-bootstrap.internal.style-links/ReactBootstrapStyle"
const baseURL = process.env.API_URL;

class ModalSignUp extends Component {
    constructor(props, context) {
        super(props, context);

        this.handleShow = this.handleShow.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.saveUser = this.saveUser.bind(this);
        this.handleInput = this.handleInput.bind(this);
        this.state = {
            show: false,
            username: "",
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

    end_signup(obj) {
    this.props.toggleLoading();
    if(obj.status===200){
        this.handleClose();
        this.props.toggleBigMessage("Completado!",
            "icon-circle-check","Ahora puede loguearse");

    }
    if(obj.status!==200){
        this.props.toggleBigMessage("Fallido!", "icon-circle-cross", "TODO: añadir msg error");

    }
}


    saveUser(e) {
        let usr =
            {
                username: this.state.username,
                email: this.state.email,
                password: this.state.password

            };
        let h = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            };

        if(this.props.addAdmin){
            usr.type_id=1;
            h.Authorization = this.props.getAuth();
        }

        this.props.toggleLoading();
        fetch('http://localhost:8000/user/', {
            method: 'POST',
            headers: h,
            body: JSON.stringify({
                username: this.state.username,
                email: this.state.email,
                password: this.state.password

            })
        }).then(r =>  r.json().then(data => ({status: r.status, body: data})))
        .then(obj => this.end_signup(obj));




    }

    render() {

        return (
            <>
                <h1><Button variant="outline-light" size="lg" onClick={this.handleShow}>
                    {!this.props.addAdmin ? 'añadir admin' : 'Sign up'}</Button></h1>

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
                            <Form.Group controlId="SignUp.username">
                                <Form.Label>Usuario</Form.Label>
                                <Form.Control value={this.state.username}
                                              name="username" type="text" placeholder="usuario"
                                              onChange={this.handleInput}/>
                            </Form.Group>
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
                        <Button variant="primary" onClick={this.saveUser}>
                            Registrarse
                        </Button>
                    </Modal.Footer>
                </Modal>
            </>
        );
    }
}

export default ModalSignUp;