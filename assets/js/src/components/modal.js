import React from 'react'
import styles from './modal_styles.css'

const modal = (props) => {
    return (
        <div className={styles.modal} style={{display: props.show ? 'block' : 'none'}}>
            <div className={styles.modal_content}>
                <div className={styles.modal_content_header}>
                    <h4>{props.title}</h4>
                    <button 
                        className="btn btn-danger btn-sm"
                        onClick={props.handleClose}>
                            <i className="fa fa-times"></i>
                    </button>
                </div>
                <div className={styles.modal_content_body}>
                    {props.children}
                </div>
            </div>
        </div>
    )
}

export default modal