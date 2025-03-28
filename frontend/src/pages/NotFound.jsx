"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import { Home } from "lucide-react";

export default function NotFoundPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="text-center">
        <h2 className="text-3xl font-extrabold text-green-600 mb-4">
          Oops! Page Not Found
        </h2>
        <p className="text-muted-foreground mb-8">
          The page you are looking for does not exist or has been moved.
        </p>
        <Button
          variant="outline"
          className="bg-green-600 hover:bg-green-700 text-white"
          onClick={() => {
            window.location.href = "/";
          }}
        >
          <Home className="mr-2" size={16} />
          Go back to homepage
        </Button>
      </div>
    </div>
  );
}
