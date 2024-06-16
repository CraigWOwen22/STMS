import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CreateBookingModal from './CreateBookingModal';
import './HomeScreen.css';

const HomeScreen = ({token}) => {
    const [bookings, setBookings] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        const fetchBookings = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/bookings/getall', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                setBookings(response.data);
            } catch (error) {
                console.error('Error fetching bookings:', error);
            }
        };
    
        fetchBookings();
    }, [token, isModalOpen]);
    

    const openModal = () => {
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
    };

    const handleDelete = async (id) => {
        try {

            const response = await axios.delete(`http://127.0.0.1:8000/bookings/${id}`);
            if (response.status === 200) {
                setBookings(bookings.filter(booking => booking.id !== id));
            } else {
                console.error('Failed to delete booking');
            }
        } catch (error) {
            console.error('Error deleting booking:', error);
        }
    };

    const handleCreateBooking = (booking) => { 
        const newBooking = {
            id: bookings.length + 1,
            section: booking.section,
            price: booking.price,
            seats: booking.seats,
            bookingDate: booking.bookingDate
        };
        setBookings([...bookings, newBooking]);
    };

    return (
        <div id="homeScreen">
            <h1>Current Bookings</h1>
            <table id="bookingsTable">
                <thead>
                    <tr>
                        <th>Section</th>
                        <th>Price(£)</th>
                        <th>Seats</th>
                        <th>Booking Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="bookingsList">
                    {bookings.map((booking) => (
                        <tr key={booking.id}>
                            <td>{booking.section}</td>
                            <td>{booking.price}</td>
                            <td>{booking.seats}</td>
                            <td>{booking.bookingDate}</td>
                            <td><button onClick={() => handleDelete(booking.id)}>Delete</button></td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <button id="openModalBtn" onClick={openModal}>Create Booking</button>
            <CreateBookingModal token = {token} show={isModalOpen} onClose={closeModal} onSubmit={handleCreateBooking} />
        </div>
    );
};

export default HomeScreen;
