import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import './checkedEvent.css';

function CheckedEvent({ show, event, token, handleClose }) {
  const [isRegistered, setIsRegistered] = useState(false);
  const [loading, setLoading] = useState(true);

  function formatTime(dateString) {
    const date = new Date(dateString);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();

    return `${hours}:${minutes} ${day}.${month}.${year}`;
  }

  useEffect(() => {
    const checkRegistration = async () => {
      setLoading(true);
      try {
        const response = await fetch(`http://127.0.0.1:8000/events/${event.id}/participants`, {
          method: 'GET',
          headers: {
            accept: 'application/json',
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          // Check if the current user is in the participants list
          const userIsRegistered = data.some((participant) => participant.is_present === true); // Assuming user_id 1 is the current user
          setIsRegistered(userIsRegistered);
        } else {
          console.error('Failed to fetch participants:', response.status);
        }
      } catch (error) {
        console.error('Error fetching participants:', error);
      } finally {
        setLoading(false);
      }
    };

    if (show && event && token) {
      checkRegistration();
    }
  }, [show, event, token]);

  const handleSubscribe = async () => {
    try {
      const method = isRegistered ? 'PATCH' : 'PATCH'; // Use DELETE to unsubscribe
      const url = `http://127.0.0.1:8000/events/${event.id}/subscribe`;

      const response = await fetch(url, {
        method: method,
        headers: {
          accept: 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setIsRegistered(!isRegistered); // Toggle registration status
        console.log(isRegistered ? 'Unsubscribed successfully!' : 'Subscribed successfully!');
        handleClose(); // Close the modal after successful action
      } else {
        console.error('Subscription failed:', response.status);
      }
    } catch (error) {
      console.error('Subscription error:', error);
    }
  };

  const buttonText = isRegistered ? 'Отписаться' : 'Записаться';

  return (
    <Modal
      show={show}
      onHide={handleClose}
      backdrop="static"
      keyboard={false}
      dialogClassName="custom-modal">
      <Modal.Header closeButton>
        <Modal.Title className="Text" style={{}}>
          {event.name}
        </Modal.Title>
      </Modal.Header>

      <Modal.Body>
        <img
          variant="top"
          style={{
            borderRadius: '20px ',
            width: '100%',
            margin: '0 0 12px',
            height: '150px',
            objectFit: 'cover',
          }}
          src={require('../../image/cardEventImg.png')}
        />
        <div style={{ display: 'flex', flexDirection: 'column', margin: '0 0 15px' }}>
          <div className="text" style={{}}>
            Описание:
          </div>
          <div className="text text-fs16">{event.description}</div>
        </div>
        <div style={{ display: 'flex', flexDirection: 'row', gap: '30px', margin: '0 0 20px' }}>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <div className="text" style={{}}>
              Тип:
            </div>
            <div className="text text-fs15">{event.event_type}</div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <div className="text" style={{}}>
              Место:
            </div>
            <div className="text text-fs15">{event.place}</div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <div className="text" style={{}}>
              Статус:
            </div>
            <div className="text text-fs15">{event.status_event}</div>
          </div>
        </div>
        <div style={{ display: 'flex', flexDirection: 'row', gap: '30px', margin: '0 0 20px' }}>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <div className="text" style={{}}>
              Время начала:
            </div>
            <div className="text text-fs15">{formatTime(event.start_time)}</div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <div className="text" style={{}}>
              Время окончания:
            </div>
            <div className="text text-fs15">{formatTime(event.end_time)}</div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <div className="text" style={{}}>
              Организатор:
            </div>
            <div className="text text-fs15">{event.organizator}</div>
          </div>
        </div>

        <div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <div className="text" style={{ margin: '0 0 10px' }}>
              Интересы:
            </div>
            <div className="text text-fs15">
              {event.interests.map((interest, index) => (
                <span
                  key={index}
                  style={{
                    display: 'inline-block',
                    padding: '8px 15px',
                    width: 'fit-content',
                    fontSize: '12px',
                    fontFamily: 'Montserrat Alternates',
                    fontWeight: '600',
                    backgroundColor: '#Ffffff',
                    borderRadius: '20px ',
                    margin: '5px',
                    boxShadow:
                      '0px 11px 3px 0px rgba(0, 0, 0, 0.00), 0px 7px 3px 0px rgba(0, 0, 0, 0.01), 0px 4px 2px 0px rgba(0, 0, 0, 0.05), 0px 2px 2px 0px rgba(0, 0, 0, 0.09), 0px 0px 1px 0px rgba(0, 0, 0, 0.10)',
                  }}>
                  {interest}
                </span>
              ))}
            </div>
          </div>
        </div>
      </Modal.Body>
      <Modal.Footer
        style={{
          display: 'flex',
          flexDirection: 'row',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
        <Button variant="" style={{ borderRadius: '15px' }} onClick={handleClose}>
          Закрыть
        </Button>
        <Button
          variant={isRegistered ? 'danger' : 'primary'}
          style={{ borderRadius: '15px' }}
          onClick={handleSubscribe}
          disabled={loading}>
          {buttonText}
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export  default CheckedEvent;
