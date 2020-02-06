import React, {Component} from 'react'
import Form from "react-bootstrap/Form";
import {Button} from "react-bootstrap";


class FormAddMoney extends Component {

    constructor(props, context) {
        super(props, context);

    //    this.handleInput = this.handleInput.bind(this);

    }


//    handleInput(event) {
//        this.setState({[event.target.name]: event.target.value})
  //  }

    render() {
        return (
            <>
                <Form>
                    <Form.Label>Enviar dinero</Form.Label>


                    <Form.Control
                        name="coin" type="text" min="1" max="10000" placeholder="moneda"
                    />

                    <Form.Control
                        name="username" type="text" min="1" max="10000" placeholder="usuario que recive"
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