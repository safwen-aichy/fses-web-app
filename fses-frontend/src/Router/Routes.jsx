// src/Router/Routes.jsx
import {
    createBrowserRouter,
} from "react-router-dom";

import Login from "../pages/Login"
import Main from "../Layout/Main";
import OfficeAssistantSystem from "../pages/OfficeAssistantSystem";
import Supervisor from "../pages/Supervisor";
import ProgramCoordinator from "../pages/ProgramCoordinator";
import PGAM from "../pages/PGAM";
import ProtectedRoute from "../components/ProtectedRoute";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Main></Main>,
        children: [
            {
                path: '/',
                element: <Login></Login>
            },
            {
                path: '/officeAssistant',
                element: (
                    <ProtectedRoute requiredRole="OFFICE_ASSISTANT">
                        <OfficeAssistantSystem />
                    </ProtectedRoute>
                )
            },
            {
                path: '/supervisor',
                element: (
                    <ProtectedRoute requiredRole="SUPERVISOR">
                        <Supervisor />
                    </ProtectedRoute>
                )
            },
            {
                path: '/programCoordinator',
                element: (
                    <ProtectedRoute requiredRole="PROGRAM_COORDINATOR">
                        <ProgramCoordinator />
                    </ProtectedRoute>
                )
            },
            {
                path: '/pgam',
                element: (
                    <ProtectedRoute requiredRole="PGAM">
                        <PGAM />
                    </ProtectedRoute>
                )
            }
        ],
    },
]);