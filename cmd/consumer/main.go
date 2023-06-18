package main

import (
	"flag"
	"log"

	"github.com/hibiken/asynq"

	"github.com/m-nny/ninetails/internal/task"
	triton "github.com/m-nny/ninetails/proto/triton/client"

	"google.golang.org/grpc"
)

var (
	redisURi  = flag.String("redis", "localhost:6379", "Redis instance URI")
	tritonUri = flag.String("triton", "localhost:8001", "Triton instance URI")
)

func init() {
	flag.Parse()
}

func main() {
	if err := runConsumer(*redisURi, *tritonUri); err != nil {
		log.Fatalf("Error running processor: %v\n", err)
	} else {
		log.Printf("consumer finished successfully\n")
	}
}

func runConsumer(redisAddr, tritonAddr string) error {
	tritonClient, err := NewTritonClient(tritonAddr)
	if err != nil {
		return err
	}
	server := asynq.NewServer(
		asynq.RedisClientOpt{Addr: redisAddr},
		asynq.Config{},
	)

	mux := asynq.NewServeMux()
	mux.Handle(task.TypeExampleSum, task.NewSumProcessor())
	mux.Handle(task.TypeInferCifar, task.NewInferCifarProcessor(tritonClient))

	return server.Run(mux)
}

func NewTritonClient(tritonAddr string) (triton.GRPCInferenceServiceClient, error) {
	conn, err := grpc.Dial(tritonAddr, grpc.WithInsecure())
	if err != nil {
		return nil, err
	}
	return triton.NewGRPCInferenceServiceClient(conn), nil
}
