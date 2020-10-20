import React from 'react'
import {useState} from 'react'
import Modal from '../../src/components/modal';
import SelectThree from '../../src/select_3';
import axios from '../../src/auth'

const productModal = (props) => {
    const [product, setProduct] = useState(null)

    return (
        <Modal title="Products"
                show={props.show}
                handleClose={props.onClose}>
            <p>Product: </p>
            <SelectThree 
                app='inventory'
                model="inventoryitem"
                onSelect={data => {
                    axios({
                        method: 'GET',
                        url: '/inventory/api/inventory-item/' + data.selected
                    }).then(res => {
                        setProduct(res.data)
                    })
                }}/>
                <br/>
            <div style={{display:'flex', width: '100%'}}>
                <div style={{flex: 1}}>
                    <p><b>Name:</b> {product ? product.name : ""}</p>
                    <p><b>Unit:</b> {product && product.unit ? product.unit.name : ""}</p>
                    <p><b>Unit Price:</b> {product ? product.unit_sales_price : ""}</p>
                </div>
                <div style={{flex: 1}}>
                    <p><b>Quantity:</b> {product ? product.qty : ""}</p>
                    <p><b>Tax:</b> {product && product.product_component.tax ? product.product_component.tax.name : ""}</p>
                </div>
            </div>
        </Modal>
    )
}

export default productModal