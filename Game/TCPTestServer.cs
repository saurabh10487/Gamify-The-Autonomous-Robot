using Complete;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class TCPTestServer : MonoBehaviour
{
    #region private members 	
    /// <summary> 	
    /// TCPListener to listen for incomming TCP connection 	
    /// requests. 	
    /// </summary> 	
    private TcpListener tcpListener;
    /// <summary> 
    /// Background thread for TcpServer workload. 	
    /// </summary> 	
    private Thread tcpListenerThread;
    /// <summary> 	
    /// Create handle to connected tcp client. 	
    /// </summary> 	
    private TcpClient connectedTcpClient;
    #endregion
    private GameObject cube1;
    public Renderer cubeRend;
    public Collider m_Collider;

    // Use this for initialization
    void Start()
    {
        gmTemp = GameObject.Find("GameManager").GetComponent<GameManager>();


        Show();
        //  GetChildWithName(GameObject.Find("CompleteLevelArt"), "Military").SetActive(true);
        //Debug.Log(cap.ToString());
        cube1 = GetChildWithName(GameObject.Find("CompleteLevelArt"), "Cube1");
        cubeRend=cube1.GetComponent<Renderer>();
        cubeRend.enabled = false;
        m_Collider = cube1.GetComponent<Collider>();
        m_Collider.enabled = false;
        // Start TcpServer background thread 		
        tcpListenerThread = new Thread(new ThreadStart(ListenForIncommingRequests));
        tcpListenerThread.IsBackground = true;
        tcpListenerThread.Start();
    }
    GameObject GetChildWithName(GameObject obj, string name)
    {
        Transform trans = obj.transform;
        Transform childTrans = trans.Find(name);
        if (childTrans != null)
        {
            return childTrans.gameObject;
        }
        else
        {
            return null;
        }
    }
    public int enbDisb = 2;

    public int countMoveF = 0;
    public int countMoveB = 0;
    public void executeBrake() {
        gmTemp.m_Tanks[1].m_Instance.GetComponent<TankMovement>().clnt.SendMessage("brake");
    }
    public void executeShoot()
    {
         gmTemp.m_Tanks[1].m_Instance.GetComponent<TankShooting>().autoFire();
         gmTemp.m_Tanks[1].m_Instance.GetComponent<TankShooting>().resetMfired();
    }
    public void MoveTankAuto_Fire(int forBack) //foreward 1 backward 2
    {
        if (forBack == 1)
        {
            if (countMoveF == 0)
            {
                for (int i = 0; i < 5; i++)
                    gmTemp.m_Tanks[1].m_Instance.GetComponent<TankMovement>().autoMove(forBack);


                Debug.Log("up...");
                gmTemp.m_Tanks[1].m_Instance.GetComponent<TankMovement>().clnt.SendMessage("up");
                Invoke("executeShoot", 1.0f);
                countMoveF = 1;
                countMoveB = 0;
            }
        }
        else if ((forBack == 2))
        {
            if (countMoveB == 0)
            {
                for (int i = 0; i < 5; i++) { 
                gmTemp.m_Tanks[1].m_Instance.GetComponent<TankMovement>().autoMove(forBack);
                }
                gmTemp.m_Tanks[1].m_Instance.GetComponent<TankMovement>().clnt.SendMessage("down");
                Invoke("executeBrake", 2.0f);

                countMoveB = 1;
                countMoveF = 0;
            }
        }

    }
    public Complete.GameManager gmTemp;
    // Update is called once per frame
    void Update()
    {
        

        if (enbDisb == 1)
        {
            cubeRend.enabled = true;
            m_Collider.enabled = true;
            if (gmTemp.allSet == true)
            {
                MoveTankAuto_Fire(1);
            }
        }
        else if (enbDisb == 0)
        {
            countMoveF = 0;
            cubeRend.enabled = false;
            m_Collider.enabled = false;
            if (gmTemp.allSet == true) { 
            MoveTankAuto_Fire(2);
        }
        }
        enbDisb = 2;
    }
    public void Show()
    {
        Debug.Log("Experiment Started, this script is working!");

    }
    /// <summary> 	
    /// Runs in background TcpServerThread; Handles incomming TcpClient requests 	
    /// </summary> 	
    private void ListenForIncommingRequests()
    {
        try
        {
            // Create listener on localhost port 8052. 			
            tcpListener = new TcpListener(IPAddress.Parse("192.168.0.104"), 22002);
            tcpListener.Start();
            Debug.Log("Server is listening");
            Byte[] bytes = new Byte[1024];
            while (true)
            {
             
                using (connectedTcpClient = tcpListener.AcceptTcpClient())
                {
                    using (NetworkStream stream = connectedTcpClient.GetStream())
                    {
                        int length;
                        while ((length = stream.Read(bytes, 0, bytes.Length)) != 0)
                        {
                            var incommingData = new byte[length];
                            Array.Copy(bytes, 0, incommingData, 0, length);
                             string clientMessage = Encoding.ASCII.GetString(incommingData);
                            Debug.Log("client message received as: " + clientMessage);
                           
                            if (clientMessage == "detected")
                            {
                                enbDisb = 1;
                            }
                            else if(clientMessage =="notdetected")
                                enbDisb = 0;




                        }
                    }
                }
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("SocketException " + socketException.ToString());
        }

    }
    /// <summary> 	
    /// Send message to client using socket connection. 	
    /// </summary> 	
    private void SendMessage()
    {
        if (connectedTcpClient == null)
        {
            return;
        }

        try
        {
            // Get a stream object for writing. 			
            NetworkStream stream = connectedTcpClient.GetStream();
            if (stream.CanWrite)
            {
                string serverMessage = "This is a message from your server.";
                // Convert string message to byte array.                 
                byte[] serverMessageAsByteArray = Encoding.ASCII.GetBytes(serverMessage);
                // Write byte array to socketConnection stream.               
                stream.Write(serverMessageAsByteArray, 0, serverMessageAsByteArray.Length);
                Debug.Log("Server sent his message - should be received by client");
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("Socket exception: " + socketException);
        }
    }
}