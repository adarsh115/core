import React from 'react'
import {useState} from 'react'
import Modal from '../../src/components/modal';
import SelectThree from '../../src/select_3';
import axios from '../../src/auth'

const customerModal = (props) => {
    const [customer, setCustomer] = useState(null)

    return (
        <Modal title="Customers"
                show={props.show}
                handleClose={props.onClose}>
            <p>Customer: </p>
            <SelectThree 
                app='invoicing'
                model="customer"
                onSelect={data => {
                    axios({
                        method: 'GET',
                        url: '/invoicing/api/customer/' + data.selected
                    }).then(res => {
                        console.log(res.data)
                        setCustomer(res.data)
                    })
                }}/>
                <br/>
            <div style={{display:'flex', width: '100%'}}>
                <div style={{flex: 1}}>
                    <p><b>Type:</b> {customer ? customer.contact.type : ""}</p>
                    <p><b>Phone:</b> {customer ? customer.contact.phone : ""}</p>
                    <p><b>Email:</b> {customer ? customer.contact.email : ""}</p>
                </div>
                <div style={{flex: 1}}>
                    <p><b>Address:</b> {customer ? customer.contact.address : ""}</p>
                </div>
            </div>
        </Modal>
    )
}

export default customerModal