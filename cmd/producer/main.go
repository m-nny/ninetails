package main

import (
	"flag"
	"log"
	"math/rand"

	"github.com/hibiken/asynq"

	"github.com/m-nny/ninetails/internal/task"
)

var redis = flag.String("redis", "localhost:6379", "Redis instance URI")

func init() {
	flag.Parse()
}

func main() {
	if err := runProducer(*redis); err != nil {
		log.Fatalf("Error running processor: %v\n", err)
	} else {
		log.Printf("Producer finished successfully\n")
	}
}

func runProducer(redisAddr string) error {
	client := asynq.NewClient(asynq.RedisClientOpt{Addr: redisAddr})
	defer client.Close()

	task, err := task.NewExampleSumPayload(rand.Intn(100), rand.Intn(100))
	if err != nil {
		return err
	}

	info, err := client.Enqueue(task)
	if err != nil {
		return err
	}
	log.Printf("enqueued task: id=%s queue=%s", info.ID, info.Queue)

	return nil
}
