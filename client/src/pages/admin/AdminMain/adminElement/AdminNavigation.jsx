import Col from 'react-bootstrap/Col';
import Nav from 'react-bootstrap/Nav';
import Row from 'react-bootstrap/Row';
import Tab from 'react-bootstrap/Tab';
import './adminNav.css'
import { EventRouteWrapper } from './createEvent/createEventAdmin';
import { Spinners } from '../../../../element/cpider/Soider';
// import ContainerEventCard from '../../../../element/card/cardEvent/CardEvent';
import CardEventAdmin from '../../../../element/card/cardEventAdmin/cardEventAdmin';
import CardStaffAdmin from '../../../../element/card/cardStaffAdmin/cardStaffAdmin' 

import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import InputGroup from 'react-bootstrap/InputGroup';



function AdminNav() {
    return (
        <div className="adminNav">
            <div className="adminNav__title">
                <h2>Административная панель</h2>
                <EventRouteWrapper />
                <div className="searchAll">
                    <InputGroup className="mb-3 searchAdmin">
                        <Form.Control
                            placeholder="Поиск"
                            aria-label="Search"
                            aria-describedby="basic-addon2"
                        />
                        <Button variant="outline-secondary" id="button-addon2">
                            Найти
                        </Button>
                    </InputGroup>
                </div>
            </div>
            <Tab.Container id="left-tabs-example" defaultActiveKey="first">
                <Row>
                    <Col sm={3}>
                        <Nav variant="pills" className="flex-column">
                            <Nav.Item>
                                <Nav.Link eventKey="1">Мероприятия</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="2">Каталог сотрудников</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="3">-------</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="4">-------</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="5">-------</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="6">-------</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="7">-------</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="8">-------</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="9">-------</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="10">-------</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="11">-------</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="12">-------</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="13">-------</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="14">-------</Nav.Link>
                            </Nav.Item>
                        </Nav>
                    </Col>
                    <Col sm={9}>
                        <Tab.Content>
                            <Tab.Pane eventKey="1">{<CardEventAdmin />}</Tab.Pane>
                            <Tab.Pane eventKey="2"><CardStaffAdmin /></Tab.Pane>
                            <Tab.Pane eventKey="3">{<Spinners />}</Tab.Pane>
                            <Tab.Pane eventKey="4">{<Spinners />}</Tab.Pane>
                            <Tab.Pane eventKey="5">{<Spinners />}</Tab.Pane>
                            <Tab.Pane eventKey="6">{<Spinners />}</Tab.Pane>
                            <Tab.Pane eventKey="7">{<Spinners />}</Tab.Pane>
                            <Tab.Pane eventKey="8">{<Spinners />}</Tab.Pane>
                            <Tab.Pane eventKey="9">{<Spinners />}</Tab.Pane>
                            <Tab.Pane eventKey="10">{<Spinners />}</Tab.Pane>
                            <Tab.Pane eventKey="11">{<Spinners />}</Tab.Pane>
                            <Tab.Pane eventKey="12">{<Spinners />}</Tab.Pane>
                            <Tab.Pane eventKey="13">{<Spinners />}</Tab.Pane>
                            <Tab.Pane eventKey="14">{<Spinners />}</Tab.Pane>
                        </Tab.Content>
                    </Col>
                </Row>
            </Tab.Container>
        </div>
    );
}

export { AdminNav };