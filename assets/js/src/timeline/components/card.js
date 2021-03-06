import React, {Component} from 'react';
import styles from '../styles.css';

class Card extends Component{
    state = {
        showOptions: false
    }

    toggleOptions = () =>{
        this.setState((prevState) =>({showOptions: !prevState.showOptions}))
    }

    render(){
        return(
            <div className={styles.timelineCard}
                style={{
                    height: this.state.showOptions ? '240px' : '120px'
                }}>
                <div className={styles.timelineCardLeft}>
                    <div className={styles.timelinePoint}></div>
                </div>
                <div className={styles.timelineCardRight}>
                    <h6 style={{fontWeight: 200}}>{this.props.timestamp}</h6>
                    <p>{this.props.title}</p>
                            
                    <span onClick={this.toggleOptions} style={{
                        padding: '6px',
                        display: 'block',
                    }}><i  className="fa fa-ellipsis-h" ></i></span>
                    <div >
                        <a target="_top" className='dropdown-item' href={"/planner/event-detail/" + this.props.id}> <i className="fas fa-file"></i> View</a>
                        <a target="_top" className='dropdown-item' href={"/planner/event-update/" + this.props.id}> <i className="fas fa-edit"></i> Edit</a>
                        <a target="_top" className='dropdown-item' href={"/planner/event-delete/" + this.props.id}> <i className="fas fa-trash"></i> Delete</a>
                    </div>
                </div>
            </div>
        )
    }
}

export default Card;