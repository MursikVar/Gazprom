import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
// import { CheckedStaff } from '../../../popUpForm/checkedStaff/CheckedEvent';
import CheckedEvent from '../../../popUpForm/checkedEvent/checkedEvent'
import './cardStaff.css'


function CardStaff({ event }) {
    

    return (
        <div className="cardStaff__wrapper">
            <a href="/checkedStaff" className="cardStaff__items" >
                <img src={require('../../../image/face.jpg')} alt="" />
                <div className="cardStaff__content">
                    <h3 className='cardStaff__content-name'>{event.username}</h3>
                    <p className='cardStaff__content-all cardStaff__content-position'>Должность: {event.position}</p>
                    <p className='cardStaff__content-all cardStaff__content-departament'>Отдел: {event.department}</p>
                    <p className='cardStaff__content-all cardStaff__content-tel'>Телефон: {event.telephone}</p>
                    <p className='cardStaff__content-all jcardStaff__content-email'>Email: {event.email}</p>
                </div>
                <ul className="cardStaff__inter">
                    <li >{event.interests}</li>
                    
                </ul>
            </a>
        </div>
    );
}

function ContainerStaffCard() {
    const [events, setEvents] = useState([]); // State for storing events
    const [show, setShow] = useState(false); // State for modal visibility
    const [selectedEvent, setSelectedEvent] = useState(null); // State for selected event

    const handleClose = () => setShow(false);
    const handleShow = (event) => {
        setSelectedEvent(event); // Set the selected event
        setShow(true); // Open the modal
    };

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/users/');
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const data = await response.json();
                setEvents(data); // Store fetched events in state
            } catch (error) {
                console.error('Error fetching events:', error);
            }
        };

        fetchEvents();
    }, []);

    return (
        <>
            <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
                {events.map((event) => (
                    <CardStaff key={event.id} event={event} handleShow={() => handleShow(event)} />
                ))}
            </div>
            {selectedEvent && (
                <CheckedEvent show={show} handleClose={handleClose} event={selectedEvent} />
            )}
        </>
    );
}

export default ContainerStaffCard;
