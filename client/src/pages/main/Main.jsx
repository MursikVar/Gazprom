import { useState, useEffect } from 'react';
import CardEvent from '../../element/card/cardEvent/CardEvent';
import ToggleButton from 'react-bootstrap/ToggleButton';
import Form from 'react-bootstrap/Form';
import moment from 'moment';
import Button from 'react-bootstrap/Button';
import CheckedEvent from '../../popUpForm/checkedEvent/checkedEvent';
import InputGroup from 'react-bootstrap/InputGroup';

import './main.css';

function Main({ token }) {
  const [selectedInterests, setSelectedInterests] = useState([]);
  const [selectedDates, setSelectedDates] = useState([]);
  const [eventId, setEventId] = useState('');
  const [url_events, setUrl_events] = useState('http://127.0.0.1:8000/events/');
  const days = [];
  const startDate = moment().startOf('month').date(10);
  const endDate = moment().endOf('month').date(23);

  const [events, setEvents] = useState([]);
  const [show, setShow] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);

  const handleClose = () => setShow(false);
  const handleShow = (event) => {
    setSelectedEvent(event);
    setShow(true);
  };

  const handleInputChange = (e) => {
    setEventId(e.target.value);
  };

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        console.log(url_events);
        const response = await fetch(url_events);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setEvents(data);
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    };

    fetchEvents();
  }, [url_events]);

  let currentDate = startDate.clone();

  while (currentDate.isSameOrBefore(endDate)) {
    days.push(currentDate.clone());
    currentDate.add(1, 'day');
  }

  const fetchEvents = async () => {
    let url = 'http://127.0.0.1:8000/events/?skip=0&limit=100&is_past=false&sort_by=date';

    if (selectedDates.length === 1) {
      const startDate = selectedDates[0];
      const endDate = moment(startDate).add(1, 'day'); // Add 1 day

      const formattedStartDate = startDate.format('YYYY-05-DDTHH:mm:ss');
      const formattedEndDate = endDate.format('YYYY-05-DDTHH:mm:ss');

      url += `&start_date=${formattedStartDate}&end_date=${formattedEndDate}`;
      setUrl_events(url);
    } else if (selectedDates.length === 2) {
      const startDate = selectedDates[0];
      const endDate = moment(selectedDates[1]).add(1, 'day'); // Add 1 day

      const formattedStartDate = startDate.format('YYYY-05-DDTHH:mm:ss');
      const formattedEndDate = endDate.format('YYYY-05-DDTHH:mm:ss');

      url += `&start_date=${formattedStartDate}&end_date=${formattedEndDate}`;
      setUrl_events(url);
    }

    const handleSearch = () => {
      if (eventId) {
        setUrl_events(
          `http://127.0.0.1:8000/events/?skip=0&limit=100&is_past=false&start_date=2025-05-10T10%3A34%3A15.04&sort_by=date`,
        );
      } else {
        setUrl_events('http://127.0.0.1:8000/events/');
      }
    };

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setEvents(data);
    } catch (e) {
    } finally {
    }
  };

  const handleDateClick = (date) => {
    setSelectedDates((prevDates) => {
      let newDates = [...prevDates];
      if (newDates.find((d) => d.isSame(date, 'day'))) {
        newDates = newDates.filter((d) => !d.isSame(date, 'day'));
      } else {
        newDates.push(date);
        newDates.sort((a, b) => a.valueOf() - b.valueOf());
        if (newDates.length > 2) {
          newDates = newDates.slice(0, 2);
        }
      }

      return newDates;
    });
  };

  useEffect(() => {
    if (selectedDates.length > 0) {
      fetchEvents();
    }
  }, [selectedDates]);

  const renderDayButton = (day) => {
    const isSelected = selectedDates.some((d) => d.isSame(day, 'day'));
    const buttonStyle = {
      borderRadius: '10px',
      margin: '5px',
      padding: '5px 10px',
      backgroundColor: isSelected ? '#007bff' : '#f8f9fa',
      color: isSelected ? 'white' : 'black',
      border: 'none',
      cursor: 'pointer',
    };

    return (
      <Button
        key={day.format('YYYY-MM-DD')}
        style={buttonStyle}
        onClick={() => handleDateClick(day)}>
        {day.format('DD')}
      </Button>
    );
  };

  const handleToggle = (interest) => {
    if (selectedInterests.includes(interest)) {
      // Remove interest if already selected
      setSelectedInterests(selectedInterests.filter((item) => item !== interest));
    } else {
      // Add interest if not already selected
      setSelectedInterests([...selectedInterests, interest]);
    }
  };

  const interestsOptions = [
    'Рекомендации',
    'Искусство',
    'Музыка',
    'Кино',
    'Наука',
    'Технологии',
    'Путешествия',
    'Еда',
    'Пение',
    'Игры',
    'Спорт',
    'Дайвинг',
    'Автомобили',
    'Головоломки',
    'Волейбол',
  ];

  return (
    <div style={{ display: 'flex', justifyContent: 'center' }}>
      <div
        className=""
        style={{
          minHeight: '800px',
          backgroundColor: '#FFFFFF',
          width: '1600px',
          padding: '26px 40px',
          borderRadius: '30px',
        }}>
        <h1 style={{ fontFamily: 'Unbounded', fontSize: '40px', margin: '0 0 20px' }}>
          Мероприятия 31 марта
        </h1>
        <div
          className=""
          style={{
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '0px',
          }}>
          <div
            className=""
            style={{
              width: '60%',
            }}>
            <div>
              <h2>Май</h2>
              <div style={{ display: 'flex', gap: '5px', marginBottom: '20px' }}>
                <div className="" style={{ fontSize: '35px' }}>
                  «
                </div>
                {days.map((day) => renderDayButton(day))}
                <div className="" style={{ fontSize: '35px' }}>
                  »
                </div>
              </div>
            </div>
          </div>
          <div
            className=""
            style={{
              width: '30%',
            }}>
            <InputGroup className="mb-3">
              <Form.Control
                placeholder="Введите id мероприятия"
                aria-label="Search"
                aria-describedby="basic-addon2"
              />
              <Button variant="outline-secondary" id="button-addon2" onClick={fetchEvents}>
                Найти
              </Button>
            </InputGroup>
          </div>
        </div>
        <div
          className=""
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'flex-start',
            width: '100%',
            height: 'auto',
            padding: '10px',
          }}>
          {interestsOptions.map((interest, index) => (
            <ToggleButton
              key={index}
              id={`toggle-${index}`}
              type="checkbox"
              variant={selectedInterests.includes(interest) ? 'primary' : 'secondary'}
              checked={selectedInterests.includes(interest)}
              value={interest}
              onChange={() => handleToggle(interest)}
              style={{
                display: 'inline-block',
                border: 'none',
                padding: '8px 15px',
                width: 'fit-content',
                fontSize: '12px',
                fontFamily: 'Montserrat Alternates',
                fontWeight: '600',
                backgroundColor: selectedInterests.includes(interest) ? '#007bff' : '#ffffff',
                borderRadius: '20px ',
                margin: '5px',
                boxShadow:
                  '0px 11px 3px 0px rgba(0, 0, 0, 0.00), 0px 7px 3px 0px rgba(0, 0, 0, 0.01), 0px 4px 2px 0px rgba(0, 0, 0, 0.05), 0px 2px 2px 0px rgba(0, 0, 0, 0.09), 0px 0px 1px 0px rgba(0, 0, 0, 0.10)',
                color: selectedInterests.includes(interest) ? '#ffffff' : '#000000',
              }}>
              {interest}
            </ToggleButton>
          ))}
        </div>

        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'start' }}>
          {events.map((event) => (
            <CardEvent key={event.id} event={event} handleShow={() => handleShow(event)} />
          ))}
        </div>
        {selectedEvent && (
          <CheckedEvent show={show} token={token} handleClose={handleClose} event={selectedEvent} />
        )}
      </div>
    </div>
  );
}

export default Main;
