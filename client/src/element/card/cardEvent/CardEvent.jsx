import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

import './cardEvent.css';

function CardEvent({ event, handleShow }) {
  function formatTime(dateString) {
    const date = new Date(dateString);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();

    return `${hours}:${minutes} ${day}.${month}.${year}`;
  }

  return (
    <Card style={{ width: '23rem', margin: '10px', borderRadius: '20px ' }}>
      <div
        className="Text"
        style={{
          width: '100%',
          position: 'absolute',
          fontSize: '15px',
          fontWeight: '500',
          display: 'flex',
          padding: '10px 10px',
          justifyContent: 'end',
        }}>
        {event.status_event}
      </div>
      <Card.Img
        variant="top"
        style={{ borderRadius: '20px 20px 0 0' }}
        src={require('../../../image/cardEventImg.png')}
      />
      <Card.Body>
        <div>
          {event.interests.map((interest, index) => (
            <div
              key={index}
              style={{
                padding: '10px 15px',
                width: 'fit-content',
                fontSize: '12px',
                fontFamily: 'Montserrat Alternates',
                fontWeight: '600',
                backgroundColor: '#F2F0F0',
                borderRadius: '20px ',
              }}>
              {interest}
            </div>
          ))}
        </div>
        <Card.Title className="Text" style={{ padding: '15px 0 5px' }}>
          {event.name}
        </Card.Title>
        <Card.Text>
          <div
            className="text"
            style={{ fontSize: '14px', fontWeight: '500', margin: '5px 0 10px' }}>
            с {formatTime(event.start_time)} по {formatTime(event.end_time)}
          </div>
          <div>Тип: {event.event_type}</div>
        </Card.Text>
        <div
          className=""
          style={{
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}>
          <div style={{ fontFamily: 'Montserrat Alternates', fontSize: '12px', fontWeight: '500' }}>
            {event.place}
          </div>
          <Button variant="primary" style={{ borderRadius: '15px' }} onClick={handleShow}>
            Подробнее
          </Button>
        </div>
      </Card.Body>
    </Card>
  );
}



export default CardEvent;
