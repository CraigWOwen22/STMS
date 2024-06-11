import React, { useState } from 'react';
import CreateBookingModal from './CreateBookingModal';
import './HomeScreen.css';

const HomeScreen = () => {
    const [bookings, setBookings] = useState([
        { id: 1, name: 'John Doe', email: 'john@example.com', date: '2024-06-01', section: 'A' },
        // Add more bookings as needed
    ]);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => {
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
    };

    const handleDelete = (id) => {
        setBookings(bookings.filter(booking => booking.id !== id));
    };

    const handleCreateBooking = (booking) => {
        const newBooking = {
            id: bookings.length + 1,
            name: 'New Booking',
            email: 'new@example.com',
            ...booking
        };
        setBookings([...bookings, newBooking]);
    };

    return (
        <div id="homeScreen">
            <h1>Current Bookings</h1>
            <table id="bookingsTable">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Date</th>
                        <th>Section</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="bookingsList">
                    {bookings.map((booking) => (
                        <tr key={booking.id}>
                            <td>{booking.name}</td>
                            <td>{booking.email}</td>
                            <td>{booking.date}</td>
                            <td>{booking.section}</td>
                            <td><button onClick={() => handleDelete(booking.id)}>Delete</button></td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <button id="openModalBtn" onClick={openModal}>Create Booking</button>
            <CreateBookingModal show={isModalOpen} onClose={closeModal} onSubmit={handleCreateBooking} />
        </div>
    );
};

export default HomeScreen;
