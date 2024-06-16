import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CreateBookingModal from './CreateBookingModal';
import './HomeScreen.css';

const HomeScreen = ({token}) => {
    const [bookings, setBookings] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);

    // Fetch all bookings related to userID from token
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
    
    // Function to track if modal should be open
    const openModal = () => {
        setIsModalOpen(true);
    };

    // Function to track if modal should be closed
    const closeModal = () => {
        setIsModalOpen(false);
    };

    // Function to delete user based on bookingID
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


    return (
        <div id="homeScreen">
            <h1>Current Bookings</h1>
            <table id="bookingsTable">
                <thead>
                    <tr>
                        <th>Theatre Section</th>
                        <th>Price (£)</th>
                        <th>Number of Seats</th>
                        <th>Booking Date</th>
                        <th>Delete?</th>
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
            <CreateBookingModal token = {token} show={isModalOpen} onClose={closeModal}/>
        </div>
    );
};

export default HomeScreen;
