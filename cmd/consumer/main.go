package main

import (
	"flag"
	"log"

	"github.com/hibiken/asynq"

	"github.com/m-nny/ninetails/internal/task"
)

var redis = flag.String("redis", "localhost:6379", "Redis instance URI")

func init() {
	flag.Parse()
}

func main() {
	if err := runConsumer(*redis); err != nil {
		log.Fatalf("Error running processor: %v\n", err)
	} else {
		log.Printf("consumer finished successfully\n")
	}
}

func runConsumer(redisAddr string) error {
	server := asynq.NewServer(
		asynq.RedisClientOpt{Addr: redisAddr},
		asynq.Config{},
	)

	mux := asynq.NewServeMux()
	mux.Handle(task.TypeExampleSum, task.NewSumProcessor())

	return server.Run(mux)
}
