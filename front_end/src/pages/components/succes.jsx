import React, {Component} from 'react'

class BigMessage extends Component {

    render() {
        return (
            <>
                <div className={"overlay"} hidden={!this.props.show}>
                    <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh'}}>

                        <span className="popup {this.props.show}"  style={{color:"while"}}>
                            <i className={this.props.icon} style={{fontSize:"80px"}}/>
                        <h1 className="popup">{this.props.text}</h1>
                            <h5 className="popup">{this.props.small_text}</h5>
                        </span>

                    </div>
                </div>
            </>
        );
    }
}

export default BigMessage;