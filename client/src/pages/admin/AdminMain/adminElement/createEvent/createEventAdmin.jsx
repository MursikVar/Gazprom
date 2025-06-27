import CreateEvent from '../../../../../popUpForm/createEvent/CreateEvent';
import { useState } from 'react';
import Button from 'react-bootstrap/Button';

function EventRouteWrapper() {
    const [showModal, setShowModal] = useState(false);
  
    const handleSave = (eventData) => {
      console.log('Сохраненные данные:', eventData);
      setShowModal(false);
    };
  
    return (
      <>
        <Button variant="primary" onClick={() => setShowModal(true)}>
          Создать мероприятие
        </Button>
  
        <CreateEvent
          show={showModal}
          onClose={() => setShowModal(false)}
          onSave={handleSave}
          onDelete={() => {
            console.log('Удаление мероприятия');
            setShowModal(false);
          }}
        />
      </>
    );
  }

  export {EventRouteWrapper}