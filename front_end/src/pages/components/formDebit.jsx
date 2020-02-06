import React, {Component} from 'react'
import Form from "react-bootstrap/Form";
import {Button} from "react-bootstrap";


class FormAddMoney extends Component {

    constructor(props, context) {
        super(props, context);

        this.handleShow = this.handleShow.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.handleInput = this.handleInput.bind(this);

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

    render() {
        return (
            <>
                <Form>
                    <Form.Label>Debitar</Form.Label>


                    <Form.Control
                        name="coin" type="text" min="1" max="10000" placeholder="moneda"
                    />

                    <Form.Control
                        name="value" type="number" min="1" max="10000" placeholder="monto"
                    />
                    <Button>Cargar</Button>
                </Form>
            </>
        );
    }
}

export default FormAddMoney;